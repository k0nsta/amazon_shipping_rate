LOAD_PAGE = """
function main(splash, args)
    splash:clear_cookies()
    splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8')
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    return {
        url = splash:url(),
        html = splash:html(),
    }
end
"""


FR_SHIPPING = """
function main(splash, args)
    splash:clear_cookies()
    splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8')
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    local click_btn = splash:select('div#glowContextualIngressPtLow_feature_div a.a-link-normal')
    click_btn.mouse_click()
    splash:wait(1)
    local post_code = splash:select('input#GLUXZipUpdateInput.GLUX_Full_Width.a-declarative'):focus()
    splash:send_keys('75001')
    local button = splash:select('span#GLUXZipUpdate.a-button.a-button-span12 span.a-button-inner.a-declarative input.a-button-input')
    button.mouse_click()
    splash:wait(1)
    splash:send_keys('<Return>')
    splash:wait(2)
    return {
        url = splash:url(),
        html = splash:html(),
    }
end
"""

UK_SHIPPING = """
unction main(splash, args)
  	splash:clear_cookies()
    splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8')
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    local shipping_link = splash:select('div#glowContextualIngressPt_feature_div a.a-link-normal')
    shipping_link.mouse_click()
    splash:wait(3)
    local postcode_field = splash:select('input#GLUXZipUpdateInput'):focus()
    splash:send_keys('WC2N <Space> 5DU')
  	splash:send_keys('<Return>')
    splash:wait(3)
  	local btn = splash:select('button[name="glowDoneButton"]'):focus()
  	splash:send_keys('<Return>')
    splash:wait(3)
  	return {
        url = splash:url(),
        html = splash:html(),
    }
end
"""

DE_SHIPPING = """
function main(splash, args)
  	splash:clear_cookies()
    splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8')
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    local shipping_link = splash:select('div#glowContextualIngressPt_feature_div a')
  	local shipping_1 = splash:select('div#oneTimeBuyBox div.a-section span.a-declarative a.a-link-normal')  
  	if not shipping_link then shipping_link = shipping_1 end
    if shipping_link then
      shipping_link.mouse_click()
      splash:wait(1)
      local postcode_field = splash:select('input#GLUXZipUpdateInput'):focus()
      splash:send_keys('10823')
      splash:send_keys('<Return>')
      splash:wait(1)
      local btn = splash:select('button[name="glowDoneButton"]'):focus()
      splash:send_keys('<Return>')
      splash:wait(2)
      return {
        url = splash:url(),
        html = splash:html(),
      }
    end
    return {
      url = splash:url(),
      html = splash:html(),
    }
end
"""