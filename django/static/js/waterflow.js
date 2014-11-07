window.onload = function(){
	var loadbox = 0;
    $('#input').keyup(function(){
        $.ajax({
            url:'/index/waterflow',
            type:"GET",
            data:{s_w:0, e_w:20},
        }).done(function(result){
            console.log(result);
            //var email = result['fields']['email'];
            //$('#show').html(email).show();
        }).fail(function(jqXHR,textStatus){
            $('#show').html('request failed '+textStatus);
        });
    });
    var data = [
					{'src':'1.jpg','title':'节目1', 'content':'我是节目1的内容，鼠标移上方时显示'},
					{'src':'2.jpg','title':'节目2'},
					{'src':'3.jpg','title':'节目3'},
					{'src':'4.jpg','title':'节目4'},
					{'src':'5.jpg','title':'节目5'},
					{'src':'6.jpg','title':'节目6'},
					{'src':'7.jpg','title':'节目7'},
					{'src':'8.jpg','title':'节目8'},
					{'src':'9.jpg','title':'节目9'},
					{'src':'10.jpg','title':'节目10', 'content':'节目10的内容'}
				];
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
		var pic = document.createElement('div');
		pic.className = 'pic';
		info.appendChild(pic);
		var img = document.createElement('img');
		img.src = '/static/images/'+data[i].src;
		img.style.height = 'auto';
		pic.appendChild(img);
		var title = document.createElement('div');
		title.className = 'title';
		info.appendChild(title);
		var a = document.createElement('a');
		a.setAttribute("href", "/program/1");
		a.innerHTML = data[i].title;
		var p = document.createElement('p');
		p.innerHTML = data[i].content;
		p.style.display = 'none';
		a.appendChild(p);
		a.onmouseover = function () {
			p = this.getElementsByTagName('p');
			p[0].style.display = 'block';
		}
		a.onmouseout = function () {
			p = this.getElementsByTagName('p');
			p[0].style.display = 'none';
		}
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
			wrap.style.width = boxW*colsNum+'px'; // the width of the wrap;
			loadbox = 1;
		}
	}	

	window.onscroll = function(){
		if(getCheck()){
            $.ajax({
                url:'/index/waterflow',
                type:"GET",
                data:{s_w:0, e_w:20},
            }).done(function(result){
                console.log(result);
                //var email = result['fields']['email'];
                //$('#show').html(email).show();
            }).fail(function(jqXHR,textStatus){
                console.log('request failed '+textStatus);
            });
            var wrap = document.getElementById('wrap');
			for(i in data){
				var box = document.createElement('div');
				box.className = 'box';
				wrap.appendChild(box);
				var info = document.createElement('div');
				info.className = 'info';
				box.appendChild(info);
				var pic = document.createElement('div');
				pic.className = 'pic';
				info.appendChild(pic);
				var img = document.createElement('img');
				img.src = '/static/images/'+data[i].src;
				img.style.height = 'auto';
				pic.appendChild(img);
				var title = document.createElement('div');
				title.className = 'title';
				info.appendChild(title);
				var a = document.createElement('a');
				a.setAttribute("href", "/program/1");
				a.innerHTML = data[i].title;
				title.appendChild(a);
			}
			PBL('wrap','box');
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