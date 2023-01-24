function updateQR(image_id, markdown_card_id){
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Token bd2149fd3ad6748f72ebae26c7ceed035af67084");

    let updated_name = prompt("Please enter updated name of the QRcode");
    
    alert(updated_name);
    // var raw = {
    //     "name": updated_name,
    //     "campaign": {
    //         "content_type": 2,
    //         "markdown_card": markdown_card_id
    //     }
    // };

    // console.log(image_id);


    var raw = `{"\n    \"name\": \"${updated_name}\",\n    \"campaign\": {\n        \"content_type\": 2,\n        \"markdown_card\": ${markdown_card_id}\n    }\n}`;
    console.log(raw);
    
    var requestOptions = {
        method: 'PUT',
        headers: myHeaders,
        body: JSON.stringify(raw),
    redirect: 'follow'
    };

    fetch("https://api.beaconstac.com/api/2.0/qrcodes/" + image_id.toString() + "/", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));

    alert("Name is changed and plage will be reloaded.");
    // location.reload();
}