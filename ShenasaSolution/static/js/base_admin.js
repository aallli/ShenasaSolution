/**
 * Created by Ali.NET on 7/5/2020.
 */

window.addEventListener('message', function(event) {
    if(event.data.event_id === 'iframe_message'){
        data = event.data.data;
        document.getElementById(data.element).style[data.style] = data.value;
    }
});