# Best Practice (distilled)

Live docs: <https://docs.blender.org/api/current/info_best_practice.html>

## Style conventions

- Follow PEP8: CamelCaps class names, lowercase underscore module names, 4-space indent,
  spaces around operators, explicit imports (no `*`), one statement per line
- Blender additions: single quotes for enums, double quotes for strings
- 79-char line limit is optional per script

## User interface layout

- If the layout declaration takes more code than the properties it draws, reconsider
- Layout variable names: `row` (`row()`), `col` (`column()`), `split` (`split()`),
  `flow` (`column_flow()`), `sub` (nested layout)
- Use `row()` for several properties on one line; `split()` only for genuinely complex layouts

## Script efficiency

- Prefer list comprehensions over in-place list surgery when filtering
  (`[p for p in mesh.polygons if len(p.vertices) != 3]`)
- `append`/`extend` at the end of lists; `pop()`/`del [-1]` for removal; `insert(0, ...)` is slow
- Avoid copying large lists (`my_list[:]` duplicates memory); prefer in-place modification
- String joining: `" ".join(...)` fastest; `"%s %s" % (...)` for formatting; avoid `+`
  concatenation in loops
- Parsing: `float(string)`/`int(string)` over `eval()`; `startswith()`/`endswith()` over slicing
- `try` is slower than `if` in hot loops — avoid exceptions in tight iteration
- `is` beats `==` when comparing the same object referenced from multiple places
- Time your code with `time.perf_counter()` while developing
