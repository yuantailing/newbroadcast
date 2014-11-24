window.onload = function(){
	var data = [];
    var num = 0;
    var loadbox = 0;
    $.ajax({
        url:'/index/waterflow',
        type:"GET",
        data:{s_w:num, e_w:num+10},
    }).done(function(result){
        data = result;
        console.log(data);
        var wrap = document.getElementById('wrap');
        var count_complete = 0;
        for(i in data) {
            //console.log(i);
            var box = document.createElement('div');
            box.className = 'box';
            wrap.appendChild(box);
            var info = document.createElement('div');
            info.className = 'info';
            box.appendChild(info);
            var pic = document.createElement('a');
            pic.className = 'pic';
            pic.setAttribute("href", "/program/" + data[i].id);
            pic.id = data[i].id;
            info.appendChild(pic);
            var img = document.createElement('img');
            img.src = data[i].src;
            img.style.height = 'auto';
            pic.appendChild(img);
            var title = document.createElement('div');
            title.className = 'title';
            pic.appendChild(title);
            var a = document.createElement('div');
            a.innerHTML = data[i].title;
            var p = document.createElement('p');
            if (data[i].content.length > 100) { 
            	p.innerHTML = data[i].content.substring(0, 100) + "...";
            } else { 
            	p.innerHTML = data[i].content;
            }
            a.appendChild(p);
            title.appendChild(a);
            img.onload = function() {
                count_complete ++;
                if (count_complete == data.length) {
                    PBL('wrap','box');
                }
            }
            if (loadbox == 0) {
                var boxs = getClass(wrap,'box'); // get all boxes;
                var boxW = boxs[0].offsetWidth; // the entHeight);width of the box;
                var colsNum = Math.floor(document.documentElement.clientWidth/boxW); // get the column number;
                wrap.style.width = boxW*colsNum +'px'; // the width of the wrap;
                loadbox = 1;
            }
        }
    }).fail(function(jqXHR,textStatus){
        console.log('request failed '+textStatus);
    });

	window.onscroll = function(){
		if(getCheck()){
            num += 10;
            $.ajax({
                url:'/index/waterflow',
                type:"GET",
                data:{s_w:num, e_w:num + 10},
            }).done(function(result){
                console.log(result);
                data = result;
                var wrap = document.getElementById('wrap');
                var count_complete = 0;
                for(i in data){
                    var box = document.createElement('div');
                    box.className = 'box';
                    wrap.appendChild(box);
                    var info = document.createElement('div');
                    info.className = 'info';
                    box.appendChild(info);
                    var pic = document.createElement('a');
                    pic.className = 'pic';
                    pic.setAttribute("href", "/program/" + data[i].id);
                    pic.id = data[i].id;
                    info.appendChild(pic);
                    var img = document.createElement('img');
                    img.src = data[i].src;
                    img.style.height = 'auto';
                    pic.appendChild(img);
                    var title = document.createElement('div');
                    title.className = 'title';
                    pic.appendChild(title);
                    var a = document.createElement('div');
                    a.innerHTML = data[i].title;
                    var p = document.createElement('p');
                    p.innerHTML = data[i].content;
                    a.appendChild(p);
                    title.appendChild(a);
                    img.onload = function() {
		                count_complete ++;
		                if (count_complete == data.length) {
		                    PBL('wrap','box');
		                }
	            	}
                }
            }).fail(function(jqXHR,textStatus){
                console.log('request failed '+ textStatus);
            });
		}
	}
}
//waterflow;
function PBL(wrap,box){
	var wrap = document.getElementById(wrap);
	var boxs  = getClass(wrap,box); // get all boxes;
	
	var boxW = boxs[0].offsetWidth; // the entHeight);width of the box;
	var colsNum = Math.floor(document.documentElement.clientWidth/boxW); // get the column number;
	wrap.style.width = boxW*colsNum+'px'; // the width of the wrap;
	var everyH = [];
	for (var i = 0; i < boxs.length; i++) {
		if(i<colsNum){
			everyH[i] = boxs[i].offsetHeight; // box's height;
			//console.log(boxs[i].offsetHeight);
		} else{
			var minH = Math.min.apply(null,everyH); // minest height;
			var minIndex = getIndex(minH,everyH); // index of the minest one;
			
			//console.log(minH + ' ' + minIndex + ' ' + everyH[minIndex]);
			getStyle(boxs[i],minH,boxs[minIndex].offsetLeft,i); 
			everyH[minIndex] += boxs[i].offsetHeight;
		}
	}
}
function getClass(wrap,className){
	var obj = wrap.getElementsByTagName('*');
	var arr = [];
	for(var i=0;i<obj.length;i++){
		if(obj[i].className == className){
			arr.push(obj[i]);
		}
	}
	return arr;
}
function getIndex(minH,everyH){
	for(index in everyH){
		if (everyH[index] == minH ) return index;
	}
}
function getCheck(){
	var documentH = document.documentElement.clientHeight;
	var scrollH = document.documentElement.scrollTop || document.body.scrollTop;
	return documentH+scrollH>=getLastH() ?true:false;
}
function getLastH(){
	var wrap = document.getElementById('wrap');
	var boxs = getClass(wrap,'box');
	return boxs[boxs.length-1].offsetTop+boxs[boxs.length-1].offsetHeight;
}
var getStartNum = 0;
function getStyle(box,top,left,index){
    if (getStartNum>=index) return;
    $(box).css({
    	'position':'absolute',
        'top':top,
        "left":left,
        "opacity":"0"
    });
    $(box).stop().animate({
        "opacity":"1"
    },999);
    getStartNum = index;
}
