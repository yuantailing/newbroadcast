	function play(pgid) {
		$.ajax({
			url:'/program/get/',
			type:'GET',
			data:{'pid':pgid},
			dataType:'json'
		}).done(function(msg) {
			changeLocalStorageToPlayer("top", "local", 1, msg.program);
		}).fail(function(jqXHR, textStatus) {
		});
		if((localStorage.hasPlayer == 0 || localStorage.hasPlayer == null)) {
			window.open("/program/play/", "_blank");
		}
	}
	
	function add(pgid) {
		$.ajax({
			url:'/program/get/',
			type:'get',
			data:{'pid':pgid},
			dataType:'json'
		}).done(function(msg) {
			changeLocalStorageToPlayer("top", "local", 0, msg.program);
		}).fail(function(jqXHR, textStatus) {
		});
		if((localStorage.hasPlayer == 0 || localStorage.hasPlayer == null)) {
			window.open("/program/play/", "_blank");
		}
	}
	
	function changeLocalStorageToPlayer(location, list, play, info) {
		var program = new Object();
		var d = new Date();
		program.time = d.getTime();
		program.id = info.id;
		program.url = info.medialink;
		program.description = info.description;
		program.title = info.title;
		if(info.piclink)
			program.thumbnail = info.piclink;
		else
			program.thumbnail = null;
		program.play = play;
		program.location = location;
		program.list = list;
		localStorage.toPlayer = JSON.stringify(program);
	}