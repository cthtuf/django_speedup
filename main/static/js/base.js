function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var app = (function(){
    var version = '0.9',
        publish = function(e){
            e.preventDefault();
            $.ajax({
                'url': $(this).attr('href'),
                'method': 'post',
            }).done(function(rpo){
                if(rpo.success == true){
                    // just to show some action with response
                    // reload page form server
                    location.reload(true)
                } else {
                    $.jGrowl("Something goes wrong. Relax and try one more time", { sticky: true });
                }
            })
        },
        showMessages = function(){
            $('.message-jgrowl').each(function(){
                $.jGrowl($(this).text());
            });
        },
        init = function(){
            showMessages();
            $('.btn-publish').on('click', publish);
            console.info('Loaded. Version: '+version);
        }
    return {
        'init': init,
    }
})();

$(function(){
    try {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        app.init();
    } catch (e){
        console.error('Something goes wrong: ' + e.message)
    }
});