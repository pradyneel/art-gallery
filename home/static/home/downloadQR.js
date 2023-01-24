// function downloadQR(url, name){
//     fetch(url).then(res => res.blob()).then(file => {
//         let tempUrl = URL.createObjectURL(file);
//         const aTag = document.createElement("a");
//         aTag.href = tempUrl;
//         aTag.download = url.replace(/^.*[\\\/]/, '');
//         document.body.appendChild(aTag);
//         aTag.click();
//         URL.revokeObjectURL(tempUrl);
//         aTag.remove();
//     }).catch(() => {
//         alert("Failed to download file!");
//     });
// }