import solara.lab
from solara import *
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import dataclasses
from typing import Any, Dict, Optional, cast

web_data = pd.read_csv("final_df.csv")
wddf = web_data.drop(columns='Unnamed: 0')
wddf.columns = wddf.columns.str.replace('cur_', '')
wddf = wddf.rename(columns={"udisc_name": "Name", "pdga_no": "PDGA#", 'rating':'Rating', 'udisc_rank':'UDisc Rank', 'udisc_index':'UDisc Index','pdga_rank':'PDGA Rank'})
wddf = wddf[['Name', 'PDGA#','Rating','UDisc Rank', 'PDGA Rank']]
wddf[['PDGA#', 'Rating', 'UDisc Rank', 'PDGA Rank']] = wddf[['PDGA#', 'Rating', 'UDisc Rank', 'PDGA Rank']].fillna(0)
wddf[['PDGA#', 'Rating', 'UDisc Rank', 'PDGA Rank']] = wddf[['PDGA#', 'Rating', 'UDisc Rank', 'PDGA Rank']].astype(int)
#board_data = pd.read_csv("cleaned_scores.csv")
#board_data['Player'] = board_data['Player'].str.rstrip('0123456789')
#bd = board_data.drop(columns='Unnamed: 0')
#print('wddf')
#print(wddf)
#print('board_data')
#print(bd)
from typing import Optional, cast
import pandas as pd
import solara.express as solara_px  # similar to plotly express, but comes with cross filters

@dataclasses.dataclass(frozen=True)
class PlayerList:
    name:str
    pdga_num:int
    rating:int
    udisc_rank:int
    pdga_rank:int

playerlist_df = pd.DataFrame()
@solara.component
def Page():
    css = """
        .v-sheet.v-sheet--tile.theme--dark.v-toolbar.v-app-bar.v-app-bar--clipped.v-app-bar--fixed.primary {
            background-color: #000000 !important;
            height: 100px !important;
        }
        
        .v-toolbar__content {
            margin: 20px!important;    
        }
        
        .v-content__wrap{
            padding-left: 20px !important;
        }
        .solara-data-table__viewport {
            margin-top: 50px !important;
        }
        """

    cell, set_cell = solara.use_state(cast(Dict[str, Any], {}))
    main_cell, set_main_cell = solara.use_state(cast(Dict[str, Any], {}))
    name, set_name = solara.use_state("")
    pdga_num, set_pdga_num = solara.use_state(0)
    rating, set_rating = solara.use_state(0)
    udisc_rank, set_udisc_rank = solara.use_state(0)
    pdga_rank, set_pdga_rank = solara.use_state(0)
    idselect = use_reactive(0)

    selected_players = use_reactive([
        PlayerList("", 0, 0, 0, 0)
    ])

    def on_action_cell(column, row_index):
        # Retrieve the values from wddf DataFrame
        set_name = wddf.iloc[row_index]['Name']
        set_pdga_num = wddf.iloc[row_index]['PDGA#']
        set_rating = wddf.iloc[row_index]['Rating']
        set_udisc_rank = wddf.iloc[row_index]['UDisc Rank']
        set_pdga_rank = wddf.iloc[row_index]['PDGA Rank']
        # Create a new PlayerList instance with the updated values
        updated_player = PlayerList(
            name=set_name,
            pdga_num=set_pdga_num,
            rating=set_rating,
            udisc_rank=set_udisc_rank,
            pdga_rank=set_pdga_rank
        )
        print("updated player selection...")
        print(updated_player)

        # Update the selected_players list at the corresponding index
        #selected_players.value[row_index] = updated_player
        selected_players.value.append(updated_player)
        print("selected_players.value")
        print(selected_players.value)
        # Optionally, you can update the playerlist_df DataFrame as well
        playerlist_df.loc[row_index] = dataclasses.asdict(updated_player)
        print(playerlist_df)



    cell_actions = [
        solara.CellAction(icon="mdi-white-balance-sunny", name="Add Data to the Table", on_click=on_action_cell)]

    # Convert PlayerList objects to dictionaries
    mysample = pd.DataFrame.from_records([dataclasses.asdict(x) for x in selected_players.value])

    # Create a DataFrame from the list of dictionaries
    playerlist_df = pd.DataFrame.from_records(mysample)
    print("playerList_df...")
    print(playerlist_df)

    # players = selected_players.value.copy()
        # players[name.value] = PlayerList(name)
        # players[pdga_num.value] = PlayerList(int(pdga_num))
        # players[rating.value] = PlayerList(int(rating))
        # players[udisc_rank.value] = PlayerList(int(udisc_rank))
        # players[pdga_rank.value] = PlayerList(int(pdga_rank))
        # selected_players.value = players
        # print(selected_players.value)





        # newdata = PlayerList(name, int(pdga_num), int(rating), int(udisc_rank), int(pdga_rank))
        # # and push to mydata.value
        # selected_players.value = [*selected_players.value, newdata]
        # for i, x in enumerate(selected_players.value):
        #     if i == row_index:
        #         set_name(x.name)
        #         print(x.name)
        #         set_pdga_num(x.pdga_num)
        #         print(x.pdga_num)
        #         set_rating(x.rating)
        #         set_udisc_rank(x.udisc_rank)
        #         set_pdga_rank(x.pdga_rank)
        #         idselect.value = row_index

        # and clear input
        # set_name("")
        # set_age("")

    #cell_actions = [solara.CellAction(icon="mdi-white-balance-sunny", name="Add Data to the Table", on_click=on_action_cell)]
    #playerlist_df = pd.DataFrame.from_records([dataclasses.asdict(x) for x in selected_players.value])

    with solara.Column() as main:
        if css:
            solara.Style(css)
        with solara.AppBarTitle():
            solara.Markdown("# <div style='color: #ffffff; margin: 10px !important; padding-top: 20px; padding-bottom: 20px; font-size: 80px;'>Disc Golf Statistics 2023</div>")
        with solara.Sidebar():
            solara.DataFrame(wddf, cell_actions=cell_actions)
        with solara.VBox():
            solara.Markdown(
                f"""
                    ## Add Players...
                    * Player: `{cell}`
                """
            )
            solara.DataFrame(playerlist_df)
            #solara.Select("Select Players for Stat Comparison...", wddf['Name'].values.tolist())
    return main








