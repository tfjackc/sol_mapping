from pathlib import Path
from typing import Optional, cast
import textwrap
import leafmap
import solara
from solara.components.file_drop import FileInfo
import pandas as pd




dgc = r"C:\Users\jcolpitt\discgolf_data\courses.gpkg"
m = leafmap.Map(center=[39.828175 -98.5795], zoom=4)
map = m.add_vector(dgc, layer_name='disc_golf_courses')


@solara.component
def Page():

    file, set_file = solara.use_state(cast(Optional[Path], None))
    path, set_path = solara.use_state(cast(Optional[Path], None))
    directory, set_directory = solara.use_state(Path("~").expanduser())

    content, set_content = solara.use_state(b"")
    filename, set_filename = solara.use_state("")
    size, set_size = solara.use_state(0)

    fields, set_fields = solara.use_state(cast(Optional[Path], None))

    with solara.VBox() as main:
        solara.Markdown("""# File Browser

        """)

        can_select = solara.ui_checkbox("Enable Select")

        def reset_path():
            set_path(None)
            set_file(None)

        def on_file(file: FileInfo):
            set_filename(file["name"])
            set_size(file["size"])
            f = file["file_obj"]
            set_content(f.read(1000))

        def get_column_names(input):
            df = pd.read_csv(input)
            set_fields(list(df.columns.values))
            print("set fields")



        solara.use_memo(reset_path, [can_select])
        solara.FileBrowser(directory, on_directory_change=set_directory, on_path_select=set_path, on_file_open=set_file, can_select=can_select)
        solara.Info(f"You are in directory: {directory}")
        solara.Info(f"You selected path: {path}")
        solara.Info(f"You opened file: {file}")

        solara.FileDrop(
            label="Drag and drop a file here to read the first 1000 bytes",
            on_file=on_file,
            lazy=True,  # We will only read the first 1000 bytes
        )
        if content:
            solara.Info(f"File {filename} has total length: {size}\n, first 100 bytes:")
            get_column_names(filename)

            with solara.Column():

                solara.Markdown(f"Field Names: {fields}")
                with solara.Row():
                    solara.DataFrame(pd.read_csv(filename), items_per_page=25)


    return main