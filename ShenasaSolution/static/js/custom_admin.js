function setDirection() {
    if (frames.length && frames[0].document && frames[0].document.getElementsByClassName('note-editable').length > 0) {
        frames[0].document.getElementsByClassName('note-editable')[0].style.direction = 'rtl';
        return;
    }
    setTimeout(function () {
        setDirection();
    }, 500);

}

setDirection();
