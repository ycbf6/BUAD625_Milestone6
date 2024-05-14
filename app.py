import streamlit as st
import pandas as pd
import os
import zipfile
import csv
import requests
from io import StringIO

st.title("Milestone 2: Fraudster Detection")
st.write("### Created by Akshay Soni")



def fetch_file_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        st.error("Failed to fetch file from URL.")
        return None

def unzip_and_get_filenames(zip_content):
    with open("temp.zip", "wb") as f:
        f.write(zip_content)
    with zipfile.ZipFile("temp.zip", "r") as zip_ref:
        file_names = [os.path.splitext(name)[0] for name in zip_ref.namelist()]
    os.remove("temp.zip")
    return file_names

def write_filenames_to_csv(file_names):
    with open("file_names.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for file_name in file_names:
            writer.writerow([file_name])


url = st.text_input("### Enter URL for Fraud Detection")
analyze_clicked = st.button("Analyze")
url_provided = bool(url)

# Fetch file content if URL provided and "Analyze" button clicked
zip_content = fetch_file_from_url(url) if analyze_clicked and url_provided else None

# Check if zip content fetched successfully
file_names = unzip_and_get_filenames(zip_content) if zip_content else None
#st.write(file_names)
# Write file names to CSV if fetched successfully
accounts_list = file_names if file_names else None

file_names_df = pd.DataFrame(file_names, columns=["custID"]).astype({"custID": "int64"}) if file_names else None




# Display success or warning messages
#st.success("File fetched successfully!") if zip_content else st.warning("Failed to fetch file. Please enter a valid URL.")
#st.success("File names extracted and saved to CSV.") if file_names else None
#st.warning("Please enter a valid URL.") if analyze_clicked and not url_provided else None



# Function to fetch CSV data from Dropbox link


# Function to fetch CSV data from Dropbox link
def fetch_data_from_dropbox(dropbox_link):
    # Send a GET request to the Dropbox link
    response = requests.get(dropbox_link)
    # Check if the request was successful
    if response.status_code == 200:
        # Read the content of the response as a string
        csv_data = StringIO(response.text)
        # Load the string data into a pandas DataFrame
        df = pd.read_csv(csv_data)
        return df
    else:
        print("Failed to fetch data from Dropbox. Please check the link.")

# Dropbox link
dropbox_link = "https://www.dropbox.com/scl/fi/uxtm3mtepms3sy7tad15c/Customer_Data.csv?rlkey=9zttslfpqaermjoesbdj5xoxi&st=yknz34v5&dl=1"

# Fetch data from Dropbox
customer_data = fetch_data_from_dropbox(dropbox_link)

# Display the fetched data
print(customer_data)


#print(file_names_df)



if file_names_df is not None and customer_data is not None:
    merged_data = pd.merge(file_names_df, customer_data, on="custID", how="left")
    merged_data = merged_data.drop(columns=["firstName", "lastName"])
    st.dataframe(merged_data)

    def get_zip_folder_name(url):
        return os.path.splitext(os.path.basename(url))[0]

    zip_folder_name = get_zip_folder_name(url)
    merged_data_filename = f"{zip_folder_name}.csv"
    st.markdown("### Download Fraudster List")
    st.download_button(label="Download", data=merged_data.to_csv(index=False).encode(), file_name=merged_data_filename, mime="text/csv")
