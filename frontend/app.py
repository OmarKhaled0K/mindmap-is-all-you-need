import streamlit as st
import json

# Initialize session state for tracking expanded nodes
if 'expanded_nodes' not in st.session_state:
    st.session_state.expanded_nodes = set()

# Your JSON data
mindmap_data = {
    "name": "LLM",
    "children": [
        {
            "name": "1. Building an LLM",
            "children": [
                { "name": "1. Data preparation and sampling" },
                { "name": "2. Choosing Transformer type" },
                { "name": "3. Attention mechanism" },
                { "name": "4. LLM Architecture" }
            ]
        },
        { 
            "name": "2. Foundation model",
            "children": [
                { "name": "1. Pre-training" },
                { "name": "2. Evaluation" }
            ]
        },
        { 
            "name": "3. Fine-tuned model",
            "children": [
                { "name": "1. Supervised fine-tuning" },
                { "name": "2. Reinforcement learning with human feedback (RLHF)" }
            ] 
        }
    ]
}

def has_children(node):
    """Check if a node has children"""
    return 'children' in node and len(node['children']) > 0

def collapse_all_children(node):
    """Recursively remove all children from expanded nodes"""
    if has_children(node):
        for child in node['children']:
            if child['name'] in st.session_state.expanded_nodes:
                st.session_state.expanded_nodes.remove(child['name'])
            collapse_all_children(child)

def toggle_node(node, parent_name=None):
    """Toggle the expanded state of a node"""
    node_name = node['name']
    
    if node_name in st.session_state.expanded_nodes:
        # Collapse this node and all its children
        st.session_state.expanded_nodes.remove(node_name)
        collapse_all_children(node)
    else:
        # Expand this node
        st.session_state.expanded_nodes.add(node_name)

def display_node(node, level=0, parent_name=None):
    """Recursively display nodes with proper indentation and arrows"""
    # Create indentation based on level
    indent = "&nbsp;" * (level * 4)
    
    # Create arrow if this is a child node
    arrow = ""
    if level > 0:
        arrow = "↳ "
    
    col1, col2 = st.columns([ level if level !=0 else 1, 1])
    
    with col2:
        # Create a unique key for the button
        button_key = f"{node['name']}_{level}"
        
        # Show parent name for child nodes
        parent_info = ""
        if parent_name and level > 0:
            parent_info = f"<br><small style='color: gray; margin-left: {level * 4}em;'>← from {parent_name}</small>"
        
        # Determine button label and functionality
        if has_children(node):
            button_label = "➖" if node['name'] in st.session_state.expanded_nodes else "➕"
            button_html = f"{indent}{arrow}<strong>{node['name']}</strong>{parent_info}"
            
            if st.button(f"{button_label} {node['name']}", key=button_key):
                toggle_node(node, parent_name)
                st.rerun()
            
            st.markdown(button_html, unsafe_allow_html=True)
            
            # Display children if expanded
            if node['name'] in st.session_state.expanded_nodes:
                for child in node['children']:
                    display_node(child, level + 1, node['name'])
        else:
            # Leaf node - no button, just text with arrow and parent info
            node_html = f"{indent}{arrow}{node['name']}{parent_info}"
            st.markdown(node_html, unsafe_allow_html=True)

def main():
    st.title("🧠 Interactive Mindmap: Large Language Models (LLM)")
    st.markdown("Click on the ➕/➖ buttons to expand/collapse sections")
    
    # Display the root node with special styling
    st.markdown(f"<h2 style='text-align: center; color: #1f77b4;'>🎯 {mindmap_data['name']}</h2>", 
                unsafe_allow_html=True)
    
    # Display all top-level children
    for child in mindmap_data['children']:
        display_node(child)
    
    # Add some controls
    st.sidebar.header("Controls")
    
    if st.sidebar.button("Expand All"):
        def expand_all_nodes(node):
            if has_children(node):
                st.session_state.expanded_nodes.add(node['name'])
                for child in node['children']:
                    expand_all_nodes(child)
        
        expand_all_nodes(mindmap_data)
        st.rerun()
    
    if st.sidebar.button("Collapse All"):
        st.session_state.expanded_nodes.clear()
        st.rerun()
    
    # Display current state
    st.sidebar.markdown("---")
    st.sidebar.write(f"**Expanded sections:** {len(st.session_state.expanded_nodes)}")
    
    # Instructions
    st.sidebar.markdown("""
    **How to use:**
    - Click **➕** to expand a section
    - Click **➖** to collapse a section (and all its children)
    - **↳** arrows show parent-child relationships
    - Gray text shows the parent of each child node
    """)

if __name__ == "__main__":
    main()