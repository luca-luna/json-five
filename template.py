
def render_template(html_file, data):
    with open(html_file) as file:
        template = file.read()
        template = replace_placeholders(template, data)
        template = render_loop(template, data)
        
        return template

def replace_placeholders(template, data):
    replaced_template = template
    
    for holder in data.keys():
        if isinstance(data[holder], str):
            replaced_template = replaced_template.replace("{{" + holder + "}}", data[holder])
            
    return replaced_template

def render_loop(template, data):
    if "loop_data" in data:
        start_tag = "{{loop}}"
        end_tag = "{{end_loop}}"
        
        start_index = template.find(start_tag)
        end_index = template.find(end_tag)
        
        start_if_tag = "{{if image}}"
        end_if_tag = "{{end_if}}"
        
        start_if_index = template.find(start_if_tag)
        end_if_index = template.find(end_if_tag)
    
        #template for the body of the loop
        loop_before_template = template[start_index + len(start_tag): start_if_index]
        if_template = template[start_if_index + len(start_if_tag): end_if_index]
        loop_after_template = template[end_if_index + len(end_if_tag): end_index]
        loop_data = data["loop_data"]
        loop_content = ""
        
        for single_content in loop_data:
            loop_content += replace_placeholders(loop_before_template, single_content)
            loop_content += replace_placeholders(if_template, single_content)
            loop_content += replace_placeholders(loop_after_template, single_content)
            
            
        final_content = template[:start_index] + loop_content + template[end_index + len(end_tag):]
        
        return final_content