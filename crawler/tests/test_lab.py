import unittest

from parameter_analyzer import analisar_parametros
from form_analyzer import analisar_formularios
from xss_detector import detectar_xss


class TestSecurityCrawler(unittest.TestCase):

    def test_parametros(self):

        url = "http://localhost/search?q=teste&page=1"

        resultado = analisar_parametros(url)

        self.assertEqual(
            resultado["quantidade"],
            2
        )

    def test_formulario(self):

        html = """
        <html>
            <body>

                <form action="/search" method="GET">

                    <input
                        type="text"
                        name="q"
                    >

                    <input
                        type="submit"
                        value="Buscar"
                    >

                </form>

            </body>
        </html>
        """

        resultado = analisar_formularios(
            "http://localhost",
            html
        )

        self.assertEqual(
            resultado["quantidade"],
            1
        )

    def test_xss_indicador(self):

        html = """
        <html>
            <script>
                document.write("teste");
            </script>
        </html>
        """

        resultado = detectar_xss(
            "http://localhost",
            html
        )

        self.assertGreater(
            len(resultado["indicadores"]),
            0
        )


if __name__ == "__main__":
    unittest.main()