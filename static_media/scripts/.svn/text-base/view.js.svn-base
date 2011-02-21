var tmpView = {	
	ready : function(){
		$('a#documentOff').toggle(
			function($e){
				$e.preventDefault();
				$('th#document').removeClass('tmpOff');
				$('th#samples').removeClass('tmpOff');
				$('th#spr').removeClass('tmpOff');
				$('th#quote').removeClass('tmpOff');
				$('td#samples').removeClass('tmpOff');
				$('td#spr').removeClass('tmpOff');
				$('td#quote').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('th#document').addClass('tmpOff');
				$('td#samples').addClass('tmpOff');
				$('td#spr').addClass('tmpOff');
				$('td#quote').addClass('tmpOff');
				$('th#samples').addClass('tmpOff');
				$('th#spr').addClass('tmpOff');
				$('th#quote').addClass('tmpOff');
			}
		);
		
		$('a#samplesOff').toggle(
			function($e){
				$e.preventDefault();
				$('td#samples').removeClass('tmpOff');
				$('th#samples').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('td#samples').addClass('tmpOff');
				$('th#samples').addClass('tmpOff');
			}
		);
		
		$('a#quotesOff').toggle(
			function($e){
				$e.preventDefault();
				$('td#quote').removeClass('tmpOff');
				$('th#quote').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('td#quote').addClass('tmpOff');
				$('th#quote').addClass('tmpOff');
			}
		);

		$('a#visitsOff').toggle(
			function($e){
				$e.preventDefault();
				$('td#visit').removeClass('tmpOff');
				$('th#visit').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('td#visit').addClass('tmpOff');
				$('th#visit').addClass('tmpOff');
			}
		);

		$('a#sprsOff').toggle(
			function($e){
				$e.preventDefault();
				$('td#spr').removeClass('tmpOff');
				$('th#spr').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('td#spr').addClass('tmpOff');
				$('th#spr').addClass('tmpOff');
			}
		);

		$('a#divisionsOff').toggle(
			function($e){
				$e.preventDefault();
				$('td#division').removeClass('tmpOff');
				$('th#division').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('td#division').addClass('tmpOff');
				$('th#division').addClass('tmpOff');
			}
		);

		$('a#regionsOff').toggle(
			function($e){
				$e.preventDefault();
				$('td#region').removeClass('tmpOff');
				$('th#region').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('td#region').addClass('tmpOff');
				$('th#region').addClass('tmpOff');
			}
		);

		$('a#segmentsOff').toggle(
			function($e){
				$e.preventDefault();
				$('td#segment').removeClass('tmpOff');
				$('th#segment').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('td#segment').addClass('tmpOff');
				$('th#segment').addClass('tmpOff');
			}
		);

		$('a#contactsOff').toggle(
			function($e){
				$e.preventDefault();
				$('th#contact').removeClass('tmpOff');
				$('td#primary_contacts').removeClass('tmpOff');
				$('td#sales_reps').removeClass('tmpOff');
				$('td#project_managers').removeClass('tmpOff');
				$('th#primary_contacts').removeClass('tmpOff');
				$('th#sales_reps').removeClass('tmpOff');
				$('th#project_managers').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('th#contact').addClass('tmpOff');
				$('td#primary_contacts').addClass('tmpOff');
				$('td#sales_reps').addClass('tmpOff');
				$('td#project_managers').addClass('tmpOff');
				$('th#primary_contacts').addClass('tmpOff');
				$('th#sales_reps').addClass('tmpOff');
				$('th#project_managers').addClass('tmpOff');
			}
		);

		$('a#timingOff').toggle(
			function($e){
				$e.preventDefault();
				$('th#timing').removeClass('tmpOff');
				$('td#timing').removeClass('tmpOff');
			},
			function($e){
				$e.preventDefault();
				$('th#timing').addClass('tmpOff');
				$('td#timing').addClass('tmpOff');
			}
		);

		$('#btnDel').attr('disabled','disabled');

		$('#btnAdd').click(function(){
			var num = $('.clonedInput').length;
			var newNum = new Number(num +1);
			var newElem = $('#input'+num).clone().attr('id', 'input'+newNum);
			newElem.children().attr('id', 'id'+newNum).attr('name', 'name' + newNum);
			$('btnDel').attr('disabled','');
			if (newNum == 10)
				$('#btnAdd').attr('disabled','disabled');
			}
		);
	}
};

$(document).ready(tmpView.ready);
