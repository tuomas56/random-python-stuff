<html>
<head>
	<title>Login</title>
	<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
	<style>
		#error {
			width: 100%;
			background: red;
		}
	</style>
</head>
<body>
	% if error is not None:
		<div id="error">{{error}}</div>
	% end
	Username: <input id="user" type="text"/><br/>
	Password: <input id="pass" type="password"/><br/>
	<button id="submit">Login</button>

	<script>
		$("#submit").click(function(e) {
			$(location).attr('href','/login/' + $("#user").val() + '/' + $('#pass').val())
		})
	</script>
</body>
</html>