# templanator/engines.py
from templanator.cdp_examples import CDPExamples


class TemplateEngine:
    """Base class for different template processing engines"""

    def process(self, source: str, template: str) -> tuple[bool, str]:
        raise NotImplementedError

    def get_example(self) -> tuple[str, str]:
        raise NotImplementedError



class TextFSMEngine(TemplateEngine):
    def get_example(self) -> tuple[str, str]:
        # Use CDP examples for TextFSM in table format
        return CDPExamples.get_example('table', 'textfsm')


class TTPEngine(TemplateEngine):
    def get_example(self) -> tuple[str, str]:
        # Use CDP examples for TTP in table format
        return CDPExamples.get_example('table', 'ttp')


class Jinja2Engine(TemplateEngine):
    def get_example(self) -> tuple[str, str]:
        source = """interface:
      name: GigabitEthernet0/1
      description: Uplink to Core
      ip: 10.0.0.1
      mask: 255.255.255.0"""

        template = """interface {{ interface.name }}
     description {{ interface.description }}
     ip address {{ interface.ip }} {{ interface.mask }}
     no shutdown"""

        return source, template

    def process(self, source: str, template: str) -> tuple[bool, str]:
        try:
            import yaml
            from jinja2 import Environment, BaseLoader

            # Parse the YAML source data
            try:
                data = yaml.safe_load(source)
            except yaml.YAMLError as e:
                return False, f"YAML parsing error: {str(e)}"

            # Setup Jinja environment
            env = Environment(loader=BaseLoader())

            # Render template
            try:
                template = env.from_string(template)
                result = template.render(**data)
                return True, result
            except Exception as e:
                return False, f"Jinja2 rendering error: {str(e)}"

        except Exception as e:
            return False, f"Jinja2 Engine Error: {str(e)}"

