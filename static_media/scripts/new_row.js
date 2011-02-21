$(document).ready(
	function(){

		var num = $('.clonedInput').length;
		$('input#id_rows').val(num);

		$('#btnAdd').click(function(){
			var num = $('.clonedInput').length;
			var newNum = new Number(num +1);
			var newElem = $('#input'+num).clone().attr('id', 'input'+newNum);
			newElem.children(':first').attr('name', 'battery_description'+newNum);
			newElem.find(':nth-child(2)').attr('name', 'type_number'+newNum);
			newElem.find(':nth-child(3)').attr('name', 'vkb_number'+newNum);
			newElem.find(':nth-child(5)').attr('name', 'quantity'+newNum);
			newElem.find(':nth-child(6)').attr('name', 'price'+newNum);
			$('input#id_rows').val(newNum);
			$('#input'+num).after(newElem);
			$('#btnDel').attr('disabled','');
			if (newNum == 10)
				$('#btnAdd').attr('disabled','disabled');
			}
		);

		$('#btnDel').click(function(){
			var num = $('.clonedInput').length;
			$('#input'+num).remove();
			$('#btnAdd').attr('disabled','');
			$('input#id_rows').val(num-1);
			if (num-1==1)
				$('#btnDel').attr('disabled','disabled');
			}
		);

	}
);

