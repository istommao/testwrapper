"""tools."""

from collections import OrderedDict

import yaml


def ordered_yaml_load(filepath, loader=yaml.Loader,
                      object_pairs_hook=OrderedDict):
    """ordered_yaml_load."""

    class OrderedLoader(loader):
        """OrderedLoader."""

    def construct_mapping(loader, node):
        """construct_mapping."""
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)

    with open(filepath) as stream:
        return yaml.load(stream, OrderedLoader)


def ordered_yaml_dump(data, stream=None, dumper=yaml.SafeDumper, **kwargs):
    """ordered_yaml_dump."""

    class OrderedDumper(dumper):
        """.OrderedDumper"""

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwargs)


def main(_data):
    import pprint
    with open('test.yaml', 'w') as _f:
        ordered_yaml_dump(
            _data, _f, default_flow_style=False, allow_unicode=True)

    with open('test.yaml') as _f:
        data = yaml.load(_f)
        pprint.pprint(data)


if __name__ == '__main__':
    data = {
        "name": "文章接口测试",
        "classname": "ArticleAPITest",
        "cases": [
            {
                "name": "get_article",
                "assertions": [{"status_code": 200}, {"errmsg": "成功"}]
            },
            {
                "name": "get_article_2",
                "assertions": [{"status_code": 400}, {"errmsg": "失败"}]
            },
        ]
    }

    main(data)
