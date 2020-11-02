const {google} = require('googleapis');
const sheets = google.sheets('v4');

async function main () {
  const authClient = await authorize();
  const request = {
    // The ID of the spreadsheet to retrieve metadata from.
    spreadsheetId: '1Alwlamox54zvT8hUqGfbqUSFXBM0raW-_nFjox8fuFU',  // TODO: Update placeholder value.

    // The ID of the developer metadata to retrieve.
    metadataId: 0,  // TODO: Update placeholder value.

    auth: authClient,
  };

  try {
    const response = (await sheets.spreadsheets.developerMetadata.get(request)).data;
    // TODO: Change code below to process the `response` object:
    console.log(JSON.stringify(response, null, 2));
  } catch (err) {
    console.error(err);
  }
}
main();

async function authorize() {
  // TODO: Change placeholder below to generate authentication credentials. See
  // https://developers.google.com/sheets/quickstart/nodejs#step_3_set_up_the_sample
  //
  // Authorize using one of the following scopes:
  //   'https://www.googleapis.com/auth/drive'
  //   'https://www.googleapis.com/auth/drive.file'
  //   'https://www.googleapis.com/auth/spreadsheets'
  let authClient = null;

  if (authClient == null) {
    throw Error('authentication failed');
  }

  return authClient;
}