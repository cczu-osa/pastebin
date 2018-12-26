dic = {'C++': 'cpp', 'Plains Text': 'text', 'aspx-cs': 'aspx-cs', 'aspx-vb': 'aspx-vb',
       'Bash': 'bash', 'Batchfile': 'bat', 'C': 'c', 'CMake': 'cmake', 'C#': 'csharp', 'CSS': 'css',
       'CSS+Django/Jinja': 'css+django', 'CSS+Ruby': 'css+erb', 'CSS+Genshi Text': 'css+genshitext',
       'CSS+Mako': 'css+mako', 'CSS+Myghty': 'css+myghty', 'CSS+PHP': 'css+php', 'CSS+Smarty': 'css+smarty',
       'Cython': 'cython', 'D': 'd', 'Delphi': 'delphi', 'Diff': 'diff', 'Django/Jinja': 'django', 'Erlang': 'erlang',
       'Fortran': 'fortran', 'Go': 'go', 'Haskell': 'haskell', 'HTML': 'html', 'HTML+Cheetah': 'html+cheetah',
       'HTML+Django/Jinja': 'html+django', 'HTML+Evoque': 'html+evoque', 'HTML+Genshi': 'html+genshi',
       'HTML+Mako': 'html+mako', 'HTML+Myghty': 'html+myghty', 'HTML+PHP': 'html+php', 'HTML+Smarty': 'html+smarty',
       'HTML+Velocity': 'html+velocity', 'haXe': 'hx', 'Hybris': 'hybris', 'Jade': 'jade', 'Java': 'java',
       'JavaScript': 'js', 'JavaScript+Cheetah': 'js+cheetah', 'JavaScript+Django/Jinja': 'js+django',
       'JavaScript+Ruby': 'js+erb', 'JavaScript+Genshi Text': 'js+genshitext', 'JavaScript+Mako': 'js+mako',
       'JavaScript+Myghty': 'js+myghty', 'JavaScript+PHP': 'js+php', 'JavaScript+Smarty': 'js+smarty',
       'Java Server Page': 'jsp', 'Literate Haskell': 'lhs', 'Lighttpd configuration file': 'lighty', 'LLVM': 'llvm',
       'Logtalk': 'logtalk', 'Lua': 'lua', 'Makefile': 'make', 'Mako': 'mako', 'MAQL': 'maql', 'Mason': 'mason',
       'Matlab': 'matlab', 'Matlab session': 'matlabsession', 'MiniD': 'minid', 'Modelica': 'modelica',
       'Modula-2': 'modula2', 'MOOCode': 'moocode', 'MuPAD': 'mupad', 'MXML': 'mxml', 'Myghty': 'myghty',
       'MySQL': 'mysql', 'NASM': 'nasm', 'Newspeak': 'newspeak', 'Nginx configuration file': 'nginx', 'NumPy': 'numpy',
       'objdump': 'objdump', 'Objective-C': 'objective-c', 'Objective-J': 'objective-j', 'OCaml': 'ocaml', 'Ooc': 'ooc',
       'Perl': 'perl', 'PHP': 'php', 'PostScript': 'postscript', 'Gettext Catalog': 'pot', 'POVRay': 'pov',
       'Prolog': 'prolog', 'Properties': 'properties', 'Python 3.0 Traceback': 'py3tb',
       'Python console session': 'pycon', 'Python Traceback': 'pytb', 'Python': 'python', 'Python 3': 'python3',
       'Ragel': 'ragel', 'Ragel in C Host': 'ragel-c', 'Ragel in CPP Host': 'ragel-cpp', 'Ragel in D Host': 'ragel-d',
       'Embedded Ragel': 'ragel-em', 'Ragel in Java Host': 'ragel-java', 'Ragel in Objective C Host': 'ragel-objc',
       'Ragel in Ruby Host': 'ragel-ruby', 'Ruby': 'rb', 'Ruby irb session': 'rbcon', 'REBOL': 'rebol',
       'Redcode': 'redcode', 'RHTML': 'rhtml', 'reStructuredText': 'rst', 'Sass': 'sass', 'Scala': 'scala',
       'Scaml': 'scaml', 'Scheme': 'scheme', 'SCSS': 'scss', 'SQL': 'sql', 'sqlite3con': 'sqlite3', 'TeX': 'tex',
       'VB.net': 'vb.net', 'XML': 'xml', 'XML+Cheetah': 'xml+cheetah', 'XML+Django/Jinja': 'xml+django',
       'XML+Ruby': 'xml+erb', 'XML+Evoque': 'xml+evoque', 'XML+Mako': 'xml+mako', 'XML+Myghty': 'xml+myghty',
       'XML+PHP': 'xml+php', 'XML+Smarty': 'xml+smarty', 'XML+Velocity': 'xml+velocity', 'XQuery': 'xquery',
       'XSLT': 'xslt', 'YAML': 'yaml'}


def get_language(lan):
    try:
        return dic[lan]
    except:
        return "text"
