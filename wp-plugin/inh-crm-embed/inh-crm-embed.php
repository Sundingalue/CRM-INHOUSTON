<?php
/**
 * Plugin Name: INH CRM Embed
 * Description: Inserta el CRM en una página mediante shortcode [inh_crm].
 * Version: 0.2.1
 * Author: In Houston Texas
 */
if (!defined('ABSPATH')) exit;
function inh_crm_embed_shortcode($atts = []){
    $defaults = ['url' => get_option('inh_crm_embed_url', 'https://crm.inhoustontexas.us'),'height' => '900px'];
    $args = shortcode_atts($defaults, $atts);
    $url = esc_url($args['url']); $height = esc_attr($args['height']);
    return '<iframe src="'.$url.'" style="width:100%;height:'.$height.';border:0;border-radius:12px;"></iframe>';
}
add_shortcode('inh_crm', 'inh_crm_embed_shortcode');
function inh_crm_embed_menu(){ add_options_page('INH CRM Embed', 'INH CRM Embed', 'manage_options', 'inh-crm-embed', 'inh_crm_embed_settings');}
add_action('admin_menu', 'inh_crm_embed_menu');
function inh_crm_embed_settings(){
    if(isset($_POST['inh_crm_embed_url'])){ update_option('inh_crm_embed_url', sanitize_text_field($_POST['inh_crm_embed_url'])); echo '<div class="updated"><p>Guardado.</p></div>'; }
    $url = esc_attr(get_option('inh_crm_embed_url', 'https://crm.inhoustontexas.us'));
    echo '<div class="wrap"><h1>INH CRM Embed</h1>';
    echo '<form method="post"><label>URL del CRM</label><br/>';
    echo '<input type="url" name="inh_crm_embed_url" value="'.$url.'" style="width:100%;max-width:600px"/><br/><br/>';
    echo '<button class="button button-primary">Guardar</button></form>';
    echo '<p>Usa el shortcode <code>[inh_crm]</code> en cualquier página.</p>';
    echo '</div>';
}
