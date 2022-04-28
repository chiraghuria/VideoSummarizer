from streamlit_option_menu import option_menu

from src import summarize_page, utils
import streamlit as st
from PIL import Image



def setup_streamlit():
    st.set_page_config(page_title="VideoTLDR", layout="wide", page_icon="🚀")
    image = Image.open('resources/videoTLDR.png')

    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image(image, width=250, caption='Converting long videos to quick reads!')
    with col3:
        st.write(' ')
    
    
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 400px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 400px;
            margin-left: -400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    apps = {
        "summarize_page": {"title": "Summarize your video", "icon": "house"}
        # "upload_transcript": {"title": "Upload Transcript", "icon": "cloud-upload"},
    }

    titles = [app["title"] for app in apps.values()]
    icons = [app["icon"] for app in apps.values()]
    params = st.experimental_get_query_params()

    if "page" in params:
        default_index = int(titles.index(params["page"][0].lower()))
    else:
        default_index = 0

    with st.sidebar:
        selected = option_menu(
            "Main Menu",
            options=titles,
            icons=icons,
            menu_icon="cast",
            default_index=default_index,
        )
    return selected


def main():
    selected = setup_streamlit()
    try:
        if selected.lower() == "summarize_page":
            summarize_page.app()
            utils.clear_all()
    except Exception as e:
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")


if __name__ == '__main__':
    main()