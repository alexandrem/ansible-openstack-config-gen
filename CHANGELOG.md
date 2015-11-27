0.3.0
=====

- Change logic to print template if condition for template variables
  - Use infer_type and add condition only for str,multi and None
  - Add condition if value is None
- Add boolean infer type

0.2.3
=====

- Convert int vars with None to 0 value

0.2.2
=====

- Added non-alphanum characters filtering for variable name
--  this now allows to generate some particular ini configs that have
    section names with *^ chars in it

0.2.1
=====

- Use new oslo_config module (oslo.config is deprecated)

0.2
====

- Fix variable names with hyphen (-)
-- Was a problem with cinder.conf zone manager

0.1
====

- Initial version
