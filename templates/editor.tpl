$def with (title, content, static_files=None)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Editing $title</title>

    $if static_files:
        $static_files


</head>
<body>


<div id="container">

<h2>Editing: $title</h2>



<div id="editor">
    <form method="POST" accept-charset="utf-8">

        <div class="wmd-panel">
            <div id="wmd-button-bar"></div>
            <textarea class="wmd-input" id="wmd-input" name="content">$content</textarea>
        </div>

        <div id="wmd-preview" class="wmd-panel wmd-preview"></div>

        <div id="toolbox">
            <input type="submit" value="Update" />
        </div>

        <p><a href="http://daringfireball.net/projects/markdown/syntax">Markdown Syntax</a></p>
    </form>
</div>

</div>


</body>
</html>