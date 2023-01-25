function updateQR(image_id){

    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Token bd2149fd3ad6748f72ebae26c7ceed035af67084");
    myHeaders.append("content-type", "application/json")

    let new_name = prompt("Enter new name for QR code");
    

    let raw = JSON.stringify({
        "name": new_name,
    });

    var requestOptions = {
    method: 'PUT',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
    };

    fetch("https://api.beaconstac.com/api/2.0/qrcodes/" + image_id.toString() + "/", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));

    alert(`QR code name updated to ${new_name}, the page will be reloaded`);
    location.reload();
}