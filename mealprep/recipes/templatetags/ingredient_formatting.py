from django import template


register = template.Library()


@register.filter
def format_ingr_quant(q: str) -> str:
    """Format ingredient quantity from float to string. Replace <1 values with ratios."""
    fract_dict = {0.25: '¼', 0.3: '⅓', 0.5: '½', 0.6: '⅔', 0.75: '¾'}
    q = float(q)
    if q in fract_dict:
        q = fract_dict[q]
    else:
        if q % 1 == 0:
            q = str(int(q))
        else:
            q = str(round(q, 1))
    return q


@register.filter
def pluralize_ingr(unit_type: str, q: int) -> str:
    """Pluralize ingredient unit if >= 2 and unit type == unité."""
    if (q >= 2) & (unit_type == 'unité'):
        return 'unités'
    else:
        return unit_type
