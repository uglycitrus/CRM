$(document).ready(
	function(){
		$('tr.link').hover(
			function(){
				$(this).addClass('tmpHighLight');
			},
			function(){
				$(this).removeClass('tmpHighLight');
			}
		);

		$('tr.link').click(
			function(){
				window.location = $(this).attr('link');
			}
		);

		$('button.link_file').click(
			function(){
				window.open($(this).attr('link'),
					'link a file',
					"resizeable=1,width=300,height=210");
				}
		);
		$('a.contact_new_popup').click(
			function(){
				window.open($(this).attr('link'),
					'new contact',
					"resizeable=1,width=300,height=210");
				}
		);
		$('a.add_contact').click(
			function(){
				window.open($(this).attr('link'),
					'add contact',
					"resizeable=1,width=300,height=210");
				}
		);
		$('table#id_primary_contact tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_primary_contact_id').value = $(this).attr('contact_id');
					window.opener.document.getElementById('id_primary_contact_name').value = $(this).attr('contact_name');
				window.close();
			}
		);
		$('table#id_sales_rep tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_sales_rep_id').value = $(this).attr('contact_id');
					window.opener.document.getElementById('id_sales_rep_name').value = $(this).attr('contact_name');
				window.close();
			}
		);
		$('table#id_project_manager tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_project_manager_id').value = $(this).attr('contact_id');
					window.opener.document.getElementById('id_project_manager_name').value = $(this).attr('contact_name');
				window.close();
			}
		);
		$('table#id_required tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_required_id').value = $(this).attr('contact_id');
					window.opener.document.getElementById('id_required_company').value = $(this).attr('contact_company');
					window.opener.document.getElementById('id_required_attention').value = $(this).attr('contact_name');
					window.opener.document.getElementById('id_required_address_line1').value = $(this).attr('contact_address_line1');
					window.opener.document.getElementById('id_required_address_line2').value = $(this).attr('contact_address_line2');
					window.opener.document.getElementById('id_required_city').value = $(this).attr('contact_city');
					window.opener.document.getElementById('id_required_state').value = $(this).attr('contact_state');
					window.opener.document.getElementById('id_required_post_code').value = $(this).attr('contact_post_code');
					window.opener.document.getElementById('id_required_phone').value = $(this).attr('contact_land_line');
					window.opener.document.getElementById('id_required_fax').value = $(this).attr('contact_fax');
					window.opener.document.getElementById('id_required_email').value = $(this).attr('contact_email');
				window.close();
			}
		);

		$('table#id_non_required tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_non_required_id').value = $(this).attr('contact_id');
					window.opener.document.getElementById('id_non_required_company').value = $(this).attr('contact_company');
					window.opener.document.getElementById('id_non_required_attention').value = $(this).attr('contact_name');
					window.opener.document.getElementById('id_non_required_address_line1').value = $(this).attr('contact_address_line1');
					window.opener.document.getElementById('id_non_required_address_line2').value = $(this).attr('contact_address_line2');
					window.opener.document.getElementById('id_non_required_city').value = $(this).attr('contact_city');
					window.opener.document.getElementById('id_non_required_state').value = $(this).attr('contact_state');
					window.opener.document.getElementById('id_non_required_post_code').value = $(this).attr('contact_post_code');
					window.opener.document.getElementById('id_non_required_phone').value = $(this).attr('contact_land_line');
				window.close();
			}
		);
		
		$('table#id_signature4 tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_signature4_id').value = $(this).attr('contact_id');
					window.opener.document.getElementById('id_signature4').value = $(this).attr('contact_name');
					window.opener.document.getElementById('id_signature4_title').value = $(this).attr('contact_title');
				window.close();
			}
		);

		$('table#id_signature3 tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_signature3_id').value = $(this).attr('contact_id');
					window.opener.document.getElementById('id_signature3').value = $(this).attr('contact_name');
					window.opener.document.getElementById('id_signature3_title').value = $(this).attr('contact_title');
				window.close();
			}
		);

		$('table#id_signature2 tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_signature2_id').value = $(this).attr('contact_id');
					window.opener.document.getElementById('id_signature2').value = $(this).attr('contact_name');
					window.opener.document.getElementById('id_signature2_title').value = $(this).attr('contact_title');
				window.close();
			}
		);

		$('table#id_signature1 tr.link').click(
			function(){
				if (window.opener && !window.opener.closed)
					window.opener.document.getElementById('id_signature1').value = $(this).attr('contact_name');
					window.opener.document.getElementById('id_signature1_title').value = $(this).attr('contact_title');
				window.close();
			}
		);

		$('#id_valid_through').datepicker({
			changeMonth: true,
			changeYear: true,
			});
		$('#id_prototype_verification').datepicker({
			changeMonth: true,
			changeYear: true,
			});
		$('#id_design_verification').datepicker({
			changeMonth: true,
			changeYear: true,
			});
		$('#id_manufacturing_verification').datepicker({
			changeMonth: true,
			changeYear: true,
			});
		$('#id_production_verification').datepicker({
			changeMonth: true,
			changeYear: true,
			});
		$('#id_end_of_life').datepicker({
			changeMonth: true,
			changeYear: true,
			});
		$('#id_date').datepicker({
			changeMonth: true,
			});		
		$('#id_inquiry_date').datepicker({
			changeMonth: true,
			});		
	}
);

