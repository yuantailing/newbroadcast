$(document).ready(function(){
    $('#login_submit').click(function(){
        $('#login_status').html("");
        $.ajax({
            url:'/login/do/',
            type:"POST",
            data:{email:$("#login-email").val(), password:$("#login-password").val()},
            dataType:"json"
        }).done(function(msg){
            if (msg.success)
                location.reload();
            else
                $('#show').text(msg.info).show();
        }).fail(function(jqXHR,textStatus){
            $('#show').html('request failed ' + textStatus);
        });
    });
});
$(document).ready(function(){
  $('#signin_submit').click(function(){
    $.ajax({
      url:'/signin/do/',
      type:"POST",
      data:{email:$("#signin-email").val(), nickname:$("#signin-nickname").val(), password:$("#signin-password").val(), password2:$("#signin-password2").val()},
      dataType:"json"
    }).done(function(msg){
      if (msg.success)
        location.reload();
      else
        $('#show2').text(msg.info).show();
    }).fail(function(jqXHR,textStatus){
      $('#show2').html('与服务器连接中断');
    });
  });
  $('#signin-email').blur(function(){
    $.ajax({
      url:'/signin/judge/',
      type:"POST",
      data:{key:$("#signin-email").val(), ptype:"email"},
      dataType:"json"
    }).done(function(msg){
        info = ""
        if (msg.exist == "true")
            info = "邮箱已存在，请重新输入"
        $('#show2').text(info).show();
    }).fail(function(jqXHR,textStatus){
      $('#show2').html('request failed '+textStatus);
    });
  });
  $('#signin-nickname').blur(function(){
    $.ajax({
      url:'/signin/judge/',
      type:"POST",
      data:{key:$("#signin-nickname").val(), ptype:"nickname"},
      dataType:"json"
      }).done(function(msg){
        info = ""
        if (msg.exist == "true")
            info = "昵称已存在，请重新输入"
        $('#show2').text(info).show();
    }).fail(function(jqXHR,textStatus){
      $('#show2').html('request failed '+textStatus);
    });
  });
});