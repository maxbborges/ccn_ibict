from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
  """
    Returns the value turned into a list.
  """
  resultado = value.split(key)
  for chave,valor in enumerate(resultado):
    if (chave<(len(resultado)-1)):
      if (valor[0]==','):
        resultado[chave]=valor[1:]

  return resultado