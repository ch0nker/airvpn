import mkdocs_gen_files
import importlib
import os

nav = mkdocs_gen_files.Nav()

nav["Introduction"] = "index.md"
nav["Changelog"] = "changelog.md"

for file in os.listdir("docs/guides"):
    name = file.capitalize()[:-3]
    path = "guides/" + file

    if file == "index.md":
        nav["Guides"] = path
        continue

    nav[("Guides", name)] = path

def get_module_name(module_name: str) -> str:
    module = importlib.import_module(module_name)
    if hasattr(module, "__title__"):
        return module.__title__
    
    return module_name.rsplit(".", 1)[-1].replace("_", " ").capitalize()

class Section:
    def __init__(self, name: str, path: str, parts: tuple = ()):
        self.name = name
        self.path = path
        self.module = self.path.replace("\\", ".").replace("/", ".")
        self.parts = parts
        self._contents = os.listdir(path)

    def create_index(self):
        name = get_module_name(self.module)
        doc_path = os.path.join(self.path, "index.md")

        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {name}\n`{self.module}`\n\n")
            fd.write(f"\n::: {self.module}\n\n")

        nav[self.parts] = doc_path

    def write(self):
        files = []
        for path in self._contents:
            if path == "__pycache__":
                continue

            if path == "__init__.py":
                self.create_index()
                continue

            full_path = os.path.join(self.path, path)
            python_path = ".".join([self.module, path])

            if os.path.isdir(full_path):
                name = get_module_name(python_path)
                section = Section(name, full_path, self.parts + (name,))
                section.write()
                continue

            files.append((full_path, python_path[:-3]))

        for full_path, python_path in files:
            name = get_module_name(python_path)
            doc_path = full_path[:-2] + "md"
            with mkdocs_gen_files.open(doc_path, "w") as fd:
                fd.write(f"# {name}\n`{python_path}`\n\n")
                fd.write(f"::: {python_path}")

            nav[self.parts + (name,)] = doc_path


section = Section("AirVPN", "airvpn", ("AirVPN",))
section.write()

with mkdocs_gen_files.open("summary.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())