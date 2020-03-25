function myFunction() {
	var request = new XMLHttpRequest();
	request.open('POST', '/api/', true);
	request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
	request.send(data);
}
