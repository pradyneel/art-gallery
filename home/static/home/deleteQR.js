function deleteQR(image_id){
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Token bd2149fd3ad6748f72ebae26c7ceed035af67084");

    var requestOptions = {
    method: 'DELETE',
    headers: myHeaders,
    redirect: 'follow'
    };

    fetch("https://api.beaconstac.com/api/2.0/qrcodes/" + image_id.toString() + "/", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));

    alert("QR code Deleted, page will be reloaded.");
    location.reload();
}