# sjdsdirectory
A simple django based api for the san juan del sur businesses

<h2>Setting up the directory</h2>
<h3>Packages needed</h3>
<ul>
<li>Django 1.6</li>
<li>Python 2.7+</li>
<li>Apache Solr
	<ul>
		<li>JRE, Jetty required</li>
	</ul>
</li>
<li>Django Haystack
	<ul>
		<li>Really important: mod_wsgi will need to be compiled for python 2.7 or greater</li>
	</ul>
</li>
<li>Removed mod_python (python.load) from Apache
	<ul>
		<li>This allowed mod_wsgi to use the correct python version</li>
		<li>Re-compiling mod_python would be most optimal, although mod_python is no long a necessity</li>
	</ul>
</li>
</ul>
