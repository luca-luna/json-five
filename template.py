
def render_template(html_file, data):
    with open(html_file) as file:
        template = file.read()
        template = replace_placeholders(template, data)
        if "loop_data2" in data.keys():
            template = render_loop_2(template, {"loop_data2": data["loop_data2"]})
        else:
            template = render_loop_2(template, {})

        return template

def replace_placeholders(template, data):
    replaced_template = template

    for holder in data.keys():
        if isinstance(data[holder], str):
            replaced_template = replaced_template.replace("{{" + holder + "}}", data[holder])

    return replaced_template

def render_loop(template, data):
    if "loop_data" in data:
        loop_start_tag = "{{loop}}"
        loop_end_tag = "{{end_loop}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)

        loop_template = template[start_index + len(loop_start_tag): end_index]
        loop_data = data["loop_data"]

        loop_content = ""
        for single_piece_of_content in loop_data:
            loop_content += replace_placeholders(loop_template, single_piece_of_content)

        final_content = template[:start_index] + loop_content + template[end_index + len(loop_end_tag):]

        return final_content
    else:
        loop_start_tag = "{{loop}}"
        loop_end_tag = "{{end_loop}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)

        final_content = template[:start_index] + template[end_index + len(loop_end_tag):]

        return final_content
    # if "loop_data" in data.keys():
    #     start_tag = "{{loop}}"
    #     end_tag = "{{end_loop}}"
    #
    #     start_index = template.find(start_tag)
    #     end_index = template.find(end_tag)
    #
    #     start_if_tag = "{{if image}}"
    #     end_if_tag = "{{end_if}}"
    #
    #     start_if_index = template.find(start_if_tag)
    #     end_if_index = template.find(end_if_tag)
    #
    #     #template for the body of the loop
    #     loop_before_template = template[start_index + len(start_tag): start_if_index]
    #     if_template = template[start_if_index + len(start_if_tag): end_if_index]
    #     loop_after_template = template[end_if_index + len(end_if_tag): end_index]
    #     loop_data = data["loop_data"]
    #     loop_content = ""
    #
    #     for single_content in loop_data:
    #         loop_content += replace_placeholders(loop_before_template, single_content)
    #         loop_content += replace_placeholders(if_template, single_content)
    #         loop_content += replace_placeholders(loop_after_template, single_content)
    #
    #
    #     final_content = template[:start_index] + loop_content + template[end_index + len(end_tag):]
    #
    #     return final_content
    # else:
    #     return template


def render_loop_2(template, data):
    if "loop_data2" in data:
        loop_start_tag = "{{loop2}}"
        loop_end_tag = "{{end_loop2}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)

        loop_template = template[start_index + len(loop_start_tag): end_index]
        loop_data = data["loop_data2"]

        loop_content = ""
        for single_piece_of_content in loop_data:
            loop_content += replace_placeholders(loop_template, single_piece_of_content)

        final_content = template[:start_index] + loop_content + template[end_index + len(loop_end_tag):]

        return final_content
    else:
        loop_start_tag = "{{loop2}}"
        loop_end_tag = "{{end_loop2}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)

        final_content = template[:start_index] + template[end_index + len(loop_end_tag):]

        return final_content