$(document).ready(function(){
    $('#login_submit').click(function(){
        $('#login_status').html("");
        $.ajax({
            url:'/login/do/',
            type:"POST",
            data:{email:$("#login-email").val(), password:$("#login-password").val()},
            dataType:"json"
        }).done(function(msg){
            $('#show').text(msg.result).show();
            $('#user-info').html("[" + msg.nickname + "],你好");
        }).fail(function(jqXHR,textStatus){
            $('#show').html('request failed ' + textStatus);
        });
    });
    $.ajax({
      url:'/login/test/',
      type:"GET",
      data:{},
        dataType:"json"
    }).done(function(msg){
      $('#login_status').text(msg.result).show();
      
    }).fail(function(jqXHR,textStatus){
      $('#login_status').html('request failed '+ textStatus);
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
      $('#show2').text(msg.info).show();
    }).fail(function(jqXHR,textStatus){
      $('#show2').html('request failed '+textStatus);
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