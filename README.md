<H1>MathTest</H1>

<H2>Usage</H2>
<ul>
    <li>pipenv install</li>
    <li>pipenv shell</li>
    <li>python MathTest.py</li>
</ul>

<H2>Tests</H2>
<ul>
    <li>pipenv install --dev</li>
    <li>pipenv shell</li>
    <li>python -m unittest</li>
    <li>coverage report -m MathTest.py helpers\RandomNonPrime.py helpers\DivisorGenerator.py</li>
</ul>

<H2>Packaging</H2>
<ul>
    <li>pipenv install --dev</li>
    <li>pipenv shell</li>
    <li>pyinstaller MathTest.py</li>
</ul>

<H2>Archiving</H2>
<ul>
    <li>git archive --format zip HEAD > MathTest.1.0.0.zip</li>
</ul>
