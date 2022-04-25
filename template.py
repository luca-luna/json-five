
def render_template(html_file, data):
    with open(html_file) as file:
        template = file.read()
        template = replace_placeholders(template, data)
        if "loop_data2" in data.keys():
            template = render_loop_2(template, {"loop_data2": data["loop_data2"]})
        else:
            template = render_loop_2(template, {})

        # if "loop_data3" in data.keys():
        #     template = render_loop_3(template, {"loop_data3": data["loop_data3"]})
        # else:
        #     template = render_loop_3(template, {})

        return template

def replace_placeholders(template, data):
    print(data, flush=True)
    replaced_template = template

    for holder in data.keys():
        print(holder, flush=True)
        if isinstance(data[holder], str):
            print("instance",flush=True)
            replaced_template = replaced_template.replace("{{" + holder + "}}", data[holder])
        elif isinstance(data[holder], int):
            print("instance", flush=True)
            replaced_template = replaced_template.replace("{{" + holder + "}}", str(data[holder]))

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

def render_loop_3(template, data):
    if "loop_data3" in data:
        loop_start_tag = "{{loop3}}"
        loop_end_tag = "{{end_loop3}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)

        loop_template = template[start_index + len(loop_start_tag): end_index]
        loop_data = data["loop_data3"]

        loop_content = ""
        for single_piece_of_content in loop_data:
            loop_content += replace_placeholders(loop_template, single_piece_of_content)

        final_content = template[:start_index] + loop_content + template[end_index + len(loop_end_tag):]

        return final_content
    else:
        loop_start_tag = "{{loop3}}"
        loop_end_tag = "{{end_loop3}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)

        final_content = template[:start_index] + template[end_index + len(loop_end_tag):]

        return final_content

