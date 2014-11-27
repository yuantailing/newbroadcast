//文件上传文件选择后事件
 $(document).ready(function() {
  $("input[id^='fileToUpload']").each(
//这里是用了each因为是多文件上传，input的id都是fileToUpload  开头
    function() {
 $("#" + $(this).attr("id") + "").live('change',function() {
 var fileName = $(this).val();
 if (fileName != null&& fileName != "") {
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
 if (!window.addEventListener) {      
    document.getElementById(fileName[j]).outerHTML+='';  //IE清除inputfile
    }else { 
     document.getElementById(fileName[j]).value = "";   //FF清除inputfile
    } 
 return false;
}
return true;
 } else {
continue;
 }
 }
  alert("文件类型不合法,只支持 jpg、gif、png、jpeg类型！");
    if (!window.addEventListener) {      
    document.getElementById(fileName[j]).outerHTML+='';  //IE
    }else { 
     document.getElementById(fileName[j]).value = "";   //FF
    } 
   return false;
  } else {
   alert("文件类型不合法,只支持 jpg、gif、png、jpeg类型！");
    if (!window.addEventListener) {      
    document.getElementById(fileName[j]).outerHTML+='';  //IE
    }else { 
     document.getElementById(fileName[j]).value = "";   //FF
    } 
   return false;
  }
 }
});
});
});
