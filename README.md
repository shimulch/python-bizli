## Bizli
![Test](https://github.com/shimulch/python-bizli/workflows/Test%20Bizli/badge.svg)

### Installation
```
pip install bizli
```

### Usage

First initialize bizli -
```
bizli init
```
This will create a ``migrations`` directory with a ``env.py`` file in it.

To create a new migration -
```
bizli create "my amazing migration"
```

To apply migrations to database -
```
bizli migrate
```

To apply rolllback migration from database -
```
bizli rollback
```

### License
MIT
