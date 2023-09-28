"""
# DataFrame

"""

from typing import Any, Dict, Optional, cast

import pandas as pd
import plotly

import solara
from solara.website.utils import apidoc
import dataclasses
df = plotly.data.iris()
newdf = pd.DataFrame()

@dataclasses.dataclass
class NewData():
    sepal_length: float
    sepal_width: float
    petal_length: float
    pedal_width: float
    species: str
    species_id: int

@solara.component
def Page():
    column, set_column = solara.use_state(cast(Optional[str], None))
    cell, set_cell = solara.use_state(cast(Dict[str, Any], {}))

    sepal_length, set_sepal_length = solara.use_state(0)
    sepal_width, set_sepal_width = solara.use_state(0)
    petal_length, set_petal_length = solara.use_state(0)
    pedal_width, set_pedal_width = solara.use_state(0)
    species, set_species = solara.use_state("")
    species_id, set_species_id = solara.use_state(0)

    def on_action_column(column):
        set_column(column)

    def on_action_cell(column, row_index):
        set_cell(dict(column=column, row_index=row_index))

        print(df.keys)

        set_sepal_length(df.iloc[row_index]['sepal_length'])
        set_sepal_width(df.iloc[row_index]['sepal_width'])
        set_petal_length(df.iloc[row_index]['petal_length'])
        set_pedal_width(df.iloc[row_index]['petal_width'])
        set_species(df.iloc[row_index]['species'])
        set_species_id(df.iloc[row_index]['species_id'])



    column_actions = [solara.ColumnAction(icon="mdi-sunglasses", name="User column action", on_click=on_action_column)]
    cell_actions = [solara.CellAction(icon="mdi-white-balance-sunny", name="User cell action", on_click=on_action_cell)]
    solara.Markdown(
        f"""
        ## Demo

        Below we show display the titanic dataset, and demonstrate a user column and cell action. Try clicking on the triple icon when hovering
        above a column or cell. And see the following values changes:

        * Column action on: `{column}`
        * Cell action on: `{cell}`
        * Sepal Length: `{sepal_length}`  # Display the value directly
        * Sepal Width: `{sepal_width}`    # Display the value directly
        * Petal Length: `{petal_length}`  # Display the value directly
        * Petal Width: `{pedal_width}`    # Display the value directly
        * Species: `{species}`
        * Species ID: `{species_id}`
        """
    )
    solara.DataFrame(df, column_actions=column_actions, cell_actions=cell_actions)


__doc__ += apidoc(solara.DataFrame.f)  # type: ignore