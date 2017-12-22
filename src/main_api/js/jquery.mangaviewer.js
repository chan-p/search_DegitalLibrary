
$(function(){
	$('body').css({'background' : '#222'});
	$('#manga-viewer').css({'width': width*2, 'margin': 'auto'});
	$('#manga-viewer img').css({'width': width});

	var view = 	Math.ceil(page/2);

	var num = 0;
	for(i=1;i<=view;i++){
		$('#manga-viewer').append('<div class="sheet" id="' + i + '"></div>');
		num+=2;
		if(num <= page) $('#'+i).append('<img id="page'+ num +'" rel="next" src="' + name + '/' + num + '.jpg">');
		num--;
		$('#'+i).append('<img id="page'+ num +'" rel="prev" src="' + name + '/' + num + '.jpg">');
		num++;
		if(i!=1) $('#'+i).hide()
		else $('#1').addClass('page-active');
	}
	$('.sheet').css({'textAlign':'center'});
	$('#manga-viewer').append('<div id="page-link" class="btn-toolbar"><div class="btn-toolbar"><div class="btn-group"><button id="btn-next" rel="next" class="btn">next</button><button id="btn-prev" rel="prev" class="btn">prev</button></div></div><div id="page-number"></div><div class="btn-toolbar"><button id="back-to-page" class="btn btn-inverse">ページを戻る</button></div></div>');
	$('.btn-toolbar').css({'clear':'both','textAlign': 'center'});
	
		
	var divide = Math.ceil(page/dividePerPage);
	num = 0;
	$('#page-number').append('<div id="btn-group' + divide +'" class="btn-group btn-page"></div>');	
	for(i=1;i<=view;i++){
		$('#page-link #btn-group'+ divide).prepend('<button class="btn ' + i +'" rel="' + i +'">'+ i +'</button>');	
		if(i%dividePerPage == 0){
				divide--;

				$('#page-number').append('<div id="btn-group' + divide + '" class="btn-group btn-page"></div>');
		}
	}
	$('button.1').addClass('btn-info');	

	
	$('.btn-page button').click(function(){
		var id = $(this).attr('rel');
		$('button').removeClass('btn-info');
		$('button.'+id).addClass('btn-info');
		$('#manga-viewer').children('.sheet').hide().removeClass('page-active');
		$('#'+id).show().addClass('page-active');
	});
	
	$('img').click(paging);
	$('#btn-next').click(paging);
	$('#btn-prev').click(paging);
	
	function paging(){
		var id = $('#manga-viewer .page-active').attr('id');
		var attr = $(this).attr('rel');
		if(attr == 'next'){
			var idNext = id;
			idNext++;
			if(idNext > view) return false;
			$('button').removeClass('btn-info');
			$('button.'+idNext).addClass('btn-info');
			$('#'+id).hide().removeClass('page-active');
			$('#'+idNext).show().addClass('page-active');
		}
		
		if(attr == 'prev'){
			var idPrev = id;
			idPrev--;
			if(idPrev <= 0) return false;
			$('button').removeClass('btn-info');
			$('button.'+idPrev).addClass('btn-info');
			$('#'+id).hide().removeClass('page-active');
			$('#'+idPrev).show().addClass('page-active');
		}

	}
	
	$('#back-to-page').click(function(){
		window.location.href = backToPage;	
	});
	
	$('.sheet img').hover(function(){
		$(this).css({'cursor': 'pointer'})
	},function(){
		$(this).css({'cursor': 'auto'})
	})

	
});