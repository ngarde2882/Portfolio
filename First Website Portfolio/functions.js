document.body.style.backgroundColor = sessionStorage.getItem('bg');
document.body.style.color = sessionStorage.getItem('cc');
function dark() {
     if ( sessionStorage.getItem('bg') === '#5D5D5D') {

            sessionStorage.setItem('bg', '#FFFFFF');
            sessionStorage.setItem('cc', '#000000');


     }
    else if (sessionStorage.getItem('bg') == null || undefined) {
        sessionStorage.setItem('bg', '#5D5D5D');
        sessionStorage.setItem('cc', '#FFFFFF');

    }
    else if( sessionStorage.getItem('bg') === '#FFFFFF') {

        sessionStorage.setItem('bg', '#5D5D5D');
        sessionStorage.setItem('cc', '#FFFFFF');


    }

document.body.style.backgroundColor = sessionStorage.getItem('bg');
document.body.style.color = sessionStorage.getItem('cc');

}