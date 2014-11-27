//文件上传文件选择后事件
$(document).ready(function() {
    $('#audio').on('change', function() {
        var fileName = $(this).val();
        if (fileName != null&& fileName != "") {
        //lastIndexOf如果没有搜索到则返回为-1
        if (fileName.lastIndexOf(".") != -1) {
            var fileType = (fileName.substring(fileName.lastIndexOf(".") + 1, 
                            fileName.length)).toLowerCase();
            var suppotFile = new Array();
            suppotFile[0] = "mp3";
            suppotFile[1] = "wav";
            suppotFile[2] = "ogg";
            for ( var i = 0; i < suppotFile.length; i++) {
                if (suppotFile[i] == fileType) {
                    if (fileName.length > 100) {
                        alert("文件名长度不能超过100字符");
                        if (!window.addEventListener)    
                            document.getElementById("audio").outerHTML+='';  //IE清除inputfile
                        else 
                            document.getElementById("audio").value = "";   //FF清除inputfile
                        return false;
                    }
                    return true;
                }
            }
            alert("文件类型不合法，只支持 mp3、wav、ogg类型的音频文件！");
            if (!window.addEventListener)
                document.getElementById("audio").outerHTML+='';  //IE
            else 
                document.getElementById("audio").value = "";   //FF
            return false;
        } else {
            alert("文件类型不合法，只支持 mp3、wav、ogg类型的音频文件！");
            if (!window.addEventListener)      
                document.getElementById("audio").outerHTML+='';  //IE
            else
                document.getElementById("audio").value = "";   //FF
        return false;
        }
        }
    });


    $("input[id^='picture']").each(function() {
        $("#" + $(this).attr("id") + "").on('change',function() {
            var fileName = $(this).val();
            if (fileName != null && fileName != "") {
            //lastIndexOf如果没有搜索到则返回为-1
                if (fileName.lastIndexOf(".") != -1) {
                    var fileType = (fileName.substring(fileName.lastIndexOf(".") + 1,
                                    fileName.length)).toLowerCase();
                    var suppotFile = new Array();
                    suppotFile[0] = "jpg";
                    suppotFile[1] = "gif";
                    suppotFile[2] = "bmp";
                    suppotFile[3] = "png";
                    suppotFile[4] = "jpeg";
                    for ( var i = 0; i < suppotFile.length; i++) {
                        if (suppotFile[i] == fileType) {
                            if (fileName.length > 100) {
                                alert("文件名长度不能超过100字符");
                                if (!window.addEventListener) 
                                    document.getElementById($(this).attr("id")).outerHTML+='';  //IE清除inputfile
                                else 
                                    document.getElementById($(this).attr("id")).value = "";   //FF清除inputfile
                                return false;
                            }
                        return true;
                        }
                    }
                    alert("文件类型不合法,只支持 jpg、gif、bmp、png、jpeg类型的图片！");
                    if (!window.addEventListener)
                        document.getElementById($(this).attr("id")).outerHTML+='';  //IE
                    else
                        document.getElementById($(this).attr("id")).value = "";   //F
                }else {
                    alert("文件类型不合法,只支持 jpg、gif、bmp、png、jpeg类型的图片！");
                    if (!window.addEventListener)      
                        document.getElementById($(this).attr("id")).outerHTML+='';  //IE
                    else
                        document.getElementById($(this).attr("id")).value = "";   //FF
                    return false;
                }
            }
        });
    });
});
