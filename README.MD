This is a template for Kaan's Flask Apps, I just like the way that this is structured.


To start the app with uswgi do this. We are using sudo because we are using port 80
`sudo uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi`
