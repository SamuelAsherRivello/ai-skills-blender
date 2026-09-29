from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/install-codex.ps1"


class InstallerTests(unittest.TestCase):
    def run_install(self, home, *args):
        return subprocess.run(["powershell.exe","-NoProfile","-File",str(SCRIPT),
                               "-UserRoot",str(home),*map(str,args)],
                              capture_output=True,text=True,timeout=30)

    def test_project_dry_conflict_backup_gallery(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)/"home"; project=Path(temp)/"project"
            args=("-Scope","Project","-ProjectPath",project,"-Skills","blender-render")
            result=self.run_install(home,*args,"-DryRun")
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertFalse(project.exists())
            result=self.run_install(home,*args)
            self.assertEqual(result.returncode,0,result.stderr)
            installed=project/".agents/skills/blender-render"
            sentinel=installed/"sentinel.txt"; sentinel.write_text("keep")
            result=self.run_install(home,*args)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(sentinel.read_text(),"keep")
            result=self.run_install(home,*args,"-Replace","-GalleryDestination",Path(temp)/"gallery")
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue(list((project/".agents/skill-backups").glob("*/sentinel.txt")))
            self.assertTrue((Path(temp)/"gallery/architectural-render-styles/images/.gitkeep").exists())
            # Installed skill validates with no reference to source checkout.
            result=subprocess.run(["python",str(ROOT/"scripts/validate-skills.py"),str(installed)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout)

    def test_user_all_and_legacy_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)
            legacy=home/".codex/skills/blender-setup"; legacy.mkdir(parents=True)
            marker=legacy/"original"; marker.write_text("preserve")
            result=self.run_install(home,"-Scope","User","-Skills","all")
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn("legacy",result.stdout)
            self.assertEqual(marker.read_text(),"preserve")
            self.assertEqual(len(list((home/".agents/skills").glob("*/SKILL.md"))),13)
            validator_copy=home/"validate-skills.py"
            validator_copy.write_bytes((ROOT/"scripts/validate-skills.py").read_bytes())
            result=subprocess.run(["python",str(validator_copy),str(home/".agents/skills")],capture_output=True,text=True,cwd=home)
            self.assertEqual(result.returncode,0,result.stdout)
            result=subprocess.run(["python",str(home/".agents/skills/blender-setup/scripts/test_check_setup.py")],capture_output=True,text=True,cwd=home)
            self.assertEqual(result.returncode,0,result.stderr)
            result=subprocess.run(["python",str(home/".agents/skills/blender-render/scripts/verify_outputs.py"),"--help"],capture_output=True,text=True,cwd=home)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_bad_selection_no_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)/"home"
            result=self.run_install(home,"-Scope","User","-Skills","../escape")
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(home.exists())

    def test_gallery_overlap_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)/"home"
            for gallery in [home, home/".agents", home/".agents/skills/blender-render"]:
                result=self.run_install(home,"-Scope","User","-Skills","blender-render",
                                        "-GalleryDestination",gallery,"-Replace")
                self.assertNotEqual(result.returncode,0)
                self.assertFalse(home.exists())

    def test_no_python_cache_installed(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)
            result=self.run_install(home,"-Scope","User","-Skills","blender-setup")
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertFalse(list((home/".agents/skills").rglob("__pycache__")))


if __name__ == "__main__":
    unittest.main()
