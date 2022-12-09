$("form[name=create_comment").submit(function(e) {
    const form = $(this);
    let res = form.find('.res');
    
    $.ajax({
        url: '/comment',
        type: "POST",
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function() {
            window.location.reload();
        },
        error: function(resp) {
            res.text(resp.responseJSON.message);
        }
    })

    e.preventDefault();
});

del_comment = () => {
    btns = $('.del_comment');

    for (let i = 0;i < btns.length;i++){
        let id = btns[i].getAttribute('data-id');

        btns[i].addEventListener("click", function(){
            $.ajax({
                url: '/comment/'+ id,
                type: "DELETE",
                success: function() {
                    window.location.reload();
                },
                error: function(resp) {
                    alert(resp.responseJSON.message);
                }
            });
        });
    }
}
del_comment();

show_edit_comment = () => {
    btns = $('.show-edit-btn');

    for (let i = 0;i < btns.length;i++){
        btn = btns[i];
        if (btn){
            let comment_id = btn.getAttribute('data-edit-id');

            btn.addEventListener("click", function(){
                show_edit_cmt = $('#edit-cmt-'+ comment_id);
                let hidden = show_edit_cmt[0].getAttribute('data-hidden');
                if (hidden == 'true'){
                    show_edit_cmt.removeClass("hidden");
                    show_edit_cmt[0].setAttribute("data-hidden", "false");
                }
                else {
                    show_edit_cmt.addClass("hidden");
                    show_edit_cmt[0].setAttribute("data-hidden", "true");
                }
            });
        }
    }
}
show_edit_comment();

$("form[name=edit_comment").submit(function(e) {
    const form = $(this);
    let res = form.find('.res');
    let id = $(this).closest("form").attr('id');
    id = id.slice(id.indexOf('-')+1);
    
    $.ajax({
        url: '/comment/'+ id,
        type: "PUT",
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function() {
            window.location.reload();
        },
        error: function(resp) {
            res.text(resp.responseJSON.message);
        }
    })

    e.preventDefault();
});