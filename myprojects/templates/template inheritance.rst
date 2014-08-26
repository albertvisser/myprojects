base.html definieert de volgende blocks:

<head>
  <title>
    block title - leeg
      gedefinieerd voor 'Doctool' + titel in base_site.html
  </title>
    block style
      block stylesheet voor admin/css/base.css
      block stylesheet_rtl voor admin/css/rtl.css
    block extrastyle - leeg
      eigen stylesheet gedefinieerd in base_site.html
    block stylesheet_ie voor admin/css/ie.css

    block extrahead - leeg
      eigen javascript gedefinieerd in base_site.html      // hoort eigenlijk niet hier
      hetzelfde eigen javascript gedefinieerd in base_app.html
    block blockbots bevat een meta tag name='robots'
</head>

<body>
  block bodyclass - leeg

  <div id='container'>
    <div id='header'>
      <div id='branding'>
        block branding - leeg
          gedefinieerd met pythoneer plaatjes in base_site.html // overbodig

          geherdefinieerd in base_app.html
      </div>

      block nav-global - leeg
        gedefinieerd met {{ menu }} in base_site.html

    </div>

    block breadcrumbs - voor div class='breadcrumbs' met link naar hoe
        gedefinieerd als leeg in base_site.html

        geherdefinieerd met if`s in base_app.html

    <div id='content'>
      block pretitle - leeg

      block content_title voor titel op de pagina
        gedefinieerd als leeg in base_site.html

        geherdefinieerd met uitgecommentaarde code in base_app.html
      block content
        blok object-tools - leeg

        {{ content}}

        geherdefinieerd in base_site.html:
          block object-tools - leeg

          block select voor {{ selector }}

          block hrule voor <br><br><hr><br>

          block startform voor {{ startform }}

          block content-data voor {{ content }}

          block endform voor {{ endform }}

        geherdefinieerd in base_app.html:
          html voor navigatie selectors

          ruimte voor melding

          block content-data
            block content-top - leeg

            block content-middle voor buttons

            block content-bottom - leeg

          html voor relatiegedeelte
      block sidebar - leeg
    </div>

    block footer voor div id='footer'
  <div>
</body>

de met // aangegeven commentaren geven aan dat deze stukjes wel uit base_site.html
verwijderd mogen worden
