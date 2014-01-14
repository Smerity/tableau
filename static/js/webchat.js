var chat_ws = new WebSocket("ws://" + SERVER_IP + "/websocket/" + window.location.pathname.substr(1).replace('/','-'));
chat_ws.onopen = function() {
}

chat_ws.onmessage = function(evt) {
    if (!$(".chat").hasClass("chat-open")){
    $(".chat .tab").addClass("notification", 1000);
    }
    $(".chat .inner").append($("<div class=\"chatbubble other\"><p></p></div>").text(evt.data));
    $('.chat .inner').scrollTop($('.chat .inner')[0].scrollHeight);
}

$(".chat").on('click', 'button', function() {
    if ($(".chat textarea").val().trim().length == 0)
        return;
    $(".chat .inner").append($("<div class=\"chatbubble\"><p></p></div>").text("You: " + $(".chat textarea").val()));
    $('.chat .inner').scrollTop($('.chat .inner')[0].scrollHeight);
    chat_ws.send($(".chat textarea").val());
    $(".chat textarea").val("");
});

$(".chat textarea").keypress(function(event) {
    if (event.keyCode == 13) { 
        event.preventDefault();
        $(".chat button").click();
    } 
}); 
           $(document).ready(function() {
            $(".chat .tab").click(function() {
            $(".chat").toggleClass("chat-open");
            $(".chat .tab").removeClass("notification");
           /* $(".chat .tab").text("<<"); */
            })
           })
