import json

import requests
import streamlit as st


def main():
    """
    Heart of the Streamlit App
    """
    # Default API Token
    api_token = ""
    # Some Basic Configuration for StreamLit
    st.set_page_config(
        page_title="GitKundli",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="auto",
    )
    # Just making sure we are not bothered by File Encoding warnings
    st.set_option("deprecation.showfileUploaderEncoding", False)
    # List of Available Web Pages to be rendered by the app
    pages = ["Home", "UserInfo", "RepoInfo", "Pull Requests"]
    p_choice = st.sidebar.selectbox("Menu", pages)
    if p_choice == "Home":
        st.title("Welcome to GitKundli")
    elif p_choice == "UserInfo":
        # User Information Page
        st.title("Want to stalk a developer on GitHub?")
        st.image(
            "https://media.giphy.com/media/LtlF03XBMZl84/giphy.gif",
            width=400,
        )
        st.write("## We got you covered! :smile:")
        acess_token = st.text_input("Enter your GitHub Token", type="password")
        username = st.text_input("Enter the username of the profile", type="default")
        if st.button("Fetch Data"):
            user_info(access_token=acess_token, username=username)


def local_css(file_name):
    """
    Function to load and render local stylesheets
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def remote_css(url):
    """
    Function to load and render remote stylesheets
    """
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    """
    Function to load and render Material Icons
    """
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def user_info(access_token, username):
    """
    Function to Fetch information about a GitHub user using Github RestAPI v3
    """
    base_url = "https://api.github.com"
    api_end_point = f"{base_url}/users/{username}"
    headers = {"Authorization": "Token " + access_token}
    try:
        # Attempting a make an request to the API
        response = requests.get(api_end_point, headers=headers)
        # Raise errors for specific error codes
        response.raise_for_status()
        # JSONify the data
        data = response.json()
        data = fix_json_values(data)
        # Now, extracting required data from the JSON for displaying!
        st.write(f"Developer Name : {data['name']}")
        st.write(f"Contact Email : {data['email']}")
        st.write(f"Currently Works at : {data['company']}")
        st.write(f"Located at : {data['location']}")
        st.write(f"Number of Public Repositories : {data['public_repos']}")
        st.write(f"Number of Public Repositories : {data['public_gists']}")
        st.write(
            f"No of developers who are following {data['name']} : {data['followers']} "
        )
        st.write(
            f"No of developers whom {data['name']} is following : {data['following']} "
        )
        st.write(f"Is {data['name']} available for hire? : {data['hireable']}")

    # Handling various kinds of errors (4xx and 5xx i.e. client side errors and server side errors)
    except requests.exceptions.HTTPError as errh:
        st.error(errh)
    except requests.exceptions.ConnectionError as errc:
        st.error(errc)
    except requests.exceptions.Timeout as errt:
        st.error(errt)
    except requests.exceptions.RequestException as err:
        st.error(err)


def fix_json_values(json_to_fix):
    """
    Function to for making certain unavailable values more readable
    """
    for k, v in json_to_fix.items():
        if str(v) == "False":
            json_to_fix[k] = "No"
        if str(v) == "None":
            json_to_fix[k] = "Not Available"
        if str(v) == "True":
            json_to_fix[k] = "Yes"
    return json_to_fix


if __name__ == "__main__":
    main()
