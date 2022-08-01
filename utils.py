import base64
import streamlit as st


def head():
    st.markdown("""
        <h2 style='text-align: center; margin-bottom: -35px;'>
        SG Car Park App \U0001F68C
        </h2>
    """, unsafe_allow_html=True
                )

    st.caption("""
        <p style='text-align: center'>
        by <a href='https://github.com/medlum'>medlum</a>
        </p>
    """, unsafe_allow_html=True
               )

    st.write("""
        <p style="font-size:25px";'text-align: center'>
        Find out how many parking lots are available!
        </p>
    """, unsafe_allow_html=True
             )


@st.cache(allow_output_mutation=True)
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_bg(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = """
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        </style>
    """ % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
