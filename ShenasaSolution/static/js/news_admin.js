/**
 * Created by Ali.NET on 6/8/2020.
 */

function truncateNews(counter) {
    if (document.getElementsByClassName("field-title").length == 0) {
        if (counter < 10)
            setTimeout(function () {
                truncateNews(counter + 1);
            }, 500);
        return;
    }

    for (let item of document.getElementsByClassName("field-title")) {
        item.innerHTML = truncateHTML(item.innerHTML, max_news_title_length);
    }
}

truncateNews(0);

function bind_selector() {
    var bias_field = document.getElementById('id_bias');
    if (!bias_field) {
        setTimeout(bind_selector, 1000);
        return;
    }

    bias_field.onchange = function () {
        document.getElementById('news_bias').className = 'bias bias' + this.value;
    }
}

bind_selector();


